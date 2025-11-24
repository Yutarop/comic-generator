def get_plot_writer_prompt(
    theme: str, additional_content: str = "up to you", num_pages: int = 4
) -> str:
    """
    Returns a prompt for generating a manga plot based on the specified theme, additional content, and number of pages.

    Args:
        theme: Manga theme (e.g., "high school rom-com", "sci-fi adventure", "horror")
        additional_content: Additional elements you want to include (e.g., "The protagonist loves cats", "Include a rain scene")
                          Default is "up to you"
        num_pages: Number of pages for the manga (1–7 pages)

    Returns:
        Complete prompt string
    """
    # Generate instructions for additional content
    if additional_content.strip().lower() == "up to you":
        content_instruction = (
            "You have complete creative freedom for the story details."
        )
    else:
        content_instruction = f"Important: Please incorporate this element into the story: {additional_content}"

    # Generate output format according to the number of pages
    output_format_lines = []
    for i in range(1, num_pages + 1):
        output_format_lines.append(f"[Page {i}] (X panels)")
        if i == 1:
            output_format_lines.append("Title: (A killer, unforgettable title)")
        output_format_lines.append(
            "→ Panel-by-panel description + dialogue + sound effects/narration as needed"
        )
        output_format_lines.append("")

    output_format = "\n".join(output_format_lines)

    return f"""
You are a legendary Japanese manga editor and story writer who has worked at Weekly Shonen Jump, Young Jump, Morning, and Champion. 
You are the mastermind behind multiple mega-hits on the level of ONE PIECE, Attack on Titan, Kaguya-sama: Love is War, Chainsaw Man, and Frieren: Beyond Journey's End.
Right now, I'm commissioning you to create a complete {num_pages}-page one-shot manga plot that absolutely blows the reader's mind.

【Strict Rules】
- Must perfectly conclude in exactly {num_pages} pages (Page 1 → Page {num_pages})
- You decide the number of panels per page freely to achieve the absolute best pacing and impact (usually 3–8 panels per page)
- It has to be so insanely good that the reader screams "HOLY SHIT!!!" even though it's only {num_pages} pages
- Page {num_pages} must deliver an explosive emotional payoff: catharsis, a mind-blowing twist, uncontrollable laughter, tears, spine-chilling horror, heart-melting romance—something that hits like a truck
- Include at least one element that makes people immediately want to re-read the whole thing
- Dialogue must feel 100% professional—natural, catchy, and memorable
- Even with minimal characters, give every single one an unforgettable personality

You must follow this exact format:
【Output Format】
{output_format}

The theme is: {theme}
{content_instruction}

Blow my mind in {num_pages} pages with this theme. Go all out.
"""
