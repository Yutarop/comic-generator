import io
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

from combine import combine_images_vertical
from prompt import get_plot_writer_prompt
from prompt_splitter import split_pages

load_dotenv()
client = genai.Client()


def generate_comic(num_pages, theme, additional_content, character_image):
    """Main function to generate a manga comic"""

    progress_bar = st.progress(0)
    status_text = st.empty()

    # Step 1: Generate plot
    status_text.text("Step 1: Generating plot...")
    progress_bar.progress(10)

    plot_writer_prompt = get_plot_writer_prompt(theme, additional_content, num_pages)

    plot_response = client.models.generate_content(
        model="gemini-3-pro-preview", contents=plot_writer_prompt
    )

    plot_text = plot_response.text

    # Step 2: Split into page prompts
    status_text.text("Step 2: Splitting into page-by-page prompts...")
    progress_bar.progress(20)

    pages_prompt = split_pages(plot_text)

    # Display generated plot
    with st.expander("📖 Generated Plot", expanded=False):
        st.text(plot_text)

    # Create chat session (image generation model)
    chat = client.chats.create(
        model="gemini-3-pro-image-preview",
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="3:4", image_size="1K"),
        ),
    )

    # Generate each page
    page_images = []
    image_files = []
    max_retries = 3

    for page_num in range(1, num_pages + 1):
        status_text.text(
            f"Step {page_num + 2}: Generating page {page_num}/{num_pages}..."
        )
        progress = 20 + (page_num / num_pages) * 60
        progress_bar.progress(int(progress))

        page_key = f"page{page_num}"
        page_generated = False
        retry_count = 0

        while not page_generated and retry_count < max_retries:
            try:
                # For page 1, include the character reference image if provided
                if page_num == 1:
                    if character_image is not None:
                        response = chat.send_message(
                            [
                                "Use this character design as a reference for the main character(s) in the manga.",
                                character_image,
                                pages_prompt[page_key],
                            ]
                        )
                    else:
                        response = chat.send_message(pages_prompt[page_key])
                else:
                    # For subsequent pages, send prompt + previous page image(s)
                    message_parts = [pages_prompt[page_key]]

                    if page_images:
                        # Reference only the most recent page
                        prev_image = Image.open(f"page{len(page_images)}_image.png")
                        message_parts.append(prev_image)

                    response = chat.send_message(message_parts)

                # Check if response and response.parts are valid
                if response is None:
                    raise ValueError("Received None response from API")
                
                if not hasattr(response, 'parts') or response.parts is None:
                    raise ValueError("Response has no valid parts attribute")

                # Save generated image
                image_found = False
                for part in response.parts:
                    if part.inline_data is not None:
                        page_image = part.as_image()
                        page_path = f"page{page_num}_image.png"
                        page_image.save(page_path)
                        page_images.append(page_image)
                        image_files.append(page_path)
                        image_found = True
                        page_generated = True
                        break
                
                if not image_found:
                    raise ValueError("No image data found in response")

            except (TypeError, ValueError, AttributeError) as e:
                retry_count += 1
                if retry_count < max_retries:
                    status_text.text(
                        f"⚠️ Error generating page {page_num}, retrying ({retry_count}/{max_retries})..."
                    )
                    st.warning(f"Retrying page {page_num} due to: {str(e)}")
                else:
                    error_msg = f"Failed to generate page {page_num} after {max_retries} attempts: {str(e)}"
                    st.error(error_msg)
                    raise RuntimeError(error_msg)
            except Exception as e:
                error_msg = f"Unexpected error generating page {page_num}: {str(e)}"
                st.error(error_msg)
                raise RuntimeError(error_msg)

    # Verify we have all pages
    if len(page_images) != num_pages:
        raise RuntimeError(
            f"Expected {num_pages} pages but only generated {len(page_images)}"
        )

    # Combine all pages vertically
    status_text.text("Final step: Combining all pages...")
    progress_bar.progress(90)

    output_file = f"{num_pages}_page_comic.png"
    combine_images_vertical(image_files, output_file)

    progress_bar.progress(100)
    status_text.text("✅ Comic generation complete!")

    return output_file, image_files


def main():
    st.set_page_config(page_title="Manga Generator", page_icon="📚", layout="wide")

    st.title("📚 AI Manga Generator")
    st.markdown("---")

    # Sidebar settings
    with st.sidebar:
        st.header("⚙️ Settings")

        # Number of pages
        num_pages = st.slider(
            "Number of Pages",
            min_value=1,
            max_value=7,
            value=4,
            help="Select the number of pages for the manga",
        )

        # Theme
        theme = st.text_input(
            "Theme",
            value="High school rom-com",
            placeholder="e.g., Sci-fi adventure, Horror, Romance",
            help="Enter the theme/genre of the manga",
        )

        # Additional instructions
        additional_content = st.text_area(
            "Additional Instructions (Optional)",
            value="",
            placeholder="e.g., The protagonist loves cats, Include a rainy scene",
            help="Add any specific elements you'd like in the story. Leave blank to let AI decide.",
        )

        if not additional_content.strip():
            additional_content = "up to you"

        # Character reference image
        st.subheader("Character Reference Image (Optional)")
        character_image_file = st.file_uploader(
            "Upload a character design reference",
            type=["png", "jpg", "jpeg"],
            help="Upload an image to use as a reference for the main character's appearance",
        )

        character_image = None
        if character_image_file is not None:
            character_image = Image.open(character_image_file)
            st.image(
                character_image,
                caption="Uploaded Image",
                use_container_width=True,
            )

        st.markdown("---")

        # Generate button
        generate_button = st.button(
            "🎨 Generate Manga", type="primary", use_container_width=True
        )

    # Main area
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📋 Current Settings")
        st.write(f"**Pages:** {num_pages}")
        st.write(f"**Theme:** {theme}")
        st.write(
            f"**Additional Instructions:** {additional_content if additional_content != 'up to you' else 'AI decides'}"
        )
        st.write(f"**Character Image:** {'Yes ✓' if character_image else 'None'}")

    with col2:
        st.subheader("ℹ️ How to Use")
        st.markdown(
            """
        1. Choose the number of pages (1–7) in the sidebar  
        2. Enter a theme (e.g., Sci-fi adventure, Horror, Rom-com)  
        3. (Optional) Add specific story elements  
        4. (Optional) Upload a character design reference image  
        5. Click **"Generate Manga"**  
        6. Once complete, view individual pages and the full comic  
        """
        )

    st.markdown("---")

    # Generation process
    if generate_button:
        if not theme.strip():
            st.error("⚠️ Please enter a theme")
            return

        try:
            with st.spinner("Generating your manga..."):
                output_file, image_files = generate_comic(
                    num_pages, theme, additional_content, character_image
                )

            st.success("🎉 Manga generated successfully!")

            # Display final combined comic
            st.subheader("📖 Completed Manga")
            final_image = Image.open(output_file)
            st.image(final_image, use_container_width=True)

            # Download button for full comic
            with open(output_file, "rb") as file:
                st.download_button(
                    label="💾 Download Full Comic",
                    data=file,
                    file_name=output_file,
                    mime="image/png",
                    use_container_width=True,
                )

            st.markdown("---")

            # Display individual pages
            st.subheader("📄 Individual Pages")
            cols = st.columns(min(num_pages, 4))

            for idx, image_path in enumerate(image_files):
                col_idx = idx % 4
                with cols[col_idx]:
                    page_image = Image.open(image_path)
                    st.image(
                        page_image,
                        caption=f"Page {idx + 1}",
                        use_container_width=True,
                    )

                    # Individual download button
                    with open(image_path, "rb") as file:
                        st.download_button(
                            label="Download",
                            data=file,
                            file_name=image_path,
                            mime="image/png",
                            key=f"download_{idx}",
                            use_container_width=True,
                        )

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("💡 Please try again. If the problem persists, try reducing the number of pages or simplifying your prompt.")
            st.exception(e)


if __name__ == "__main__":
    main()