def get_plot_writer_prompt(
    theme: str, additional_content: str = "up to you", num_pages: int = 4, language: str = "English"
) -> str:
    """
    Returns a prompt for generating a manga plot based on the specified theme, additional content, number of pages, and language.

    Args:
        theme: Manga theme (e.g., "high school rom-com", "sci-fi adventure", "horror")
        additional_content: Additional elements you want to include (e.g., "The protagonist loves cats", "Include a rain scene")
                          Default is "up to you"
        num_pages: Number of pages for the manga (1–7 pages)
        language: Language for the manga content - "English" or "Japanese" (default: "English")

    Returns:
        Complete prompt string in the specified language
    """
    if language == "Japanese":
        return _get_japanese_prompt(theme, additional_content, num_pages)
    else:
        return _get_english_prompt(theme, additional_content, num_pages)


def _get_english_prompt(theme: str, additional_content: str, num_pages: int) -> str:
    """Returns the English version of the prompt"""
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
- ALL DIALOGUE, NARRATION, AND TEXT MUST BE IN ENGLISH

You must follow this exact format:
【Output Format】
{output_format}

The theme is: {theme}
{content_instruction}

Blow my mind in {num_pages} pages with this theme. Go all out.
"""


def _get_japanese_prompt(theme: str, additional_content: str, num_pages: int) -> str:
    """Returns the Japanese version of the prompt"""
    # Generate instructions for additional content
    if additional_content.strip().lower() == "up to you":
        content_instruction = "ストーリーの詳細は完全にあなたの創作の自由です。"
    else:
        content_instruction = f"重要: この要素をストーリーに取り入れてください: {additional_content}"

    # Generate output format according to the number of pages
    output_format_lines = []
    for i in range(1, num_pages + 1):
        output_format_lines.append(f"[Page {i}] (X panels)")
        if i == 1:
            output_format_lines.append("タイトル: (キャッチーで忘れられないタイトル)")
        output_format_lines.append(
            "→ コマごとの描写 + セリフ + 必要に応じて効果音/ナレーション"
        )
        output_format_lines.append("")

    output_format = "\n".join(output_format_lines)

    return f"""
あなたは週刊少年ジャンプ、ヤングジャンプ、モーニング、チャンピオンで活躍してきた伝説的な漫画編集者・ストーリー作家です。
ONE PIECE、進撃の巨人、かぐや様は告らせたい、チェンソーマン、葬送のフリーレンレベルのメガヒット作を何本も手がけた名手です。
今、{num_pages}ページの読み切り漫画のプロットを作成してください。読者の心を完全に掴む作品をお願いします。

【厳守事項】
- 必ず{num_pages}ページで完璧に完結させること(1ページ目 → {num_pages}ページ目)
- 各ページのコマ数は最高の演出とテンポを実現するため自由に決定してください(通常1ページあたり3〜8コマ)
- 日本の漫画は基本的に右から左へ読み進めるため、横にコマを並べる際は右から左に物語を進めること
- たった{num_pages}ページでも読者が「すげええええ!!!」と叫ぶほどの圧倒的な面白さを実現すること
- {num_pages}ページ目では爆発的な感情のカタルシスを届けること: カタルシス、衝撃的などんでん返し、爆笑、涙、背筋も凍る恐怖、胸キュンロマンスなど、心に突き刺さる何かを
- 読み終わった後すぐにもう一度読み返したくなる要素を少なくとも1つ入れること
- セリフは100%プロフェッショナルな水準で: 自然で、キャッチーで、印象に残るものにすること
- 登場人物が少なくても、全員に忘れられない個性を持たせること
- 全てのセリフ、ナレーション、テキストは必ず日本語で書くこと

必ず以下のフォーマットに従ってください:
【出力フォーマット】
{output_format}

テーマは: {theme}
{content_instruction}

{num_pages}ページでこのテーマを最高に面白く描いてください。全力で行け。
"""