"""Gradio UI for seed-song recommendations."""

from __future__ import annotations

import gradio as gr

from music_recs import ListeningCatalog, recommend_songs
from music_recs.data import load_catalog_frames

tracks, artists, albums = load_catalog_frames()
CATALOG = ListeningCatalog(tracks, artists, albums)


def recommend_from_text(seed_text: str, count: int) -> str:
    seeds = [line.strip() for line in seed_text.splitlines() if line.strip()]
    if not seeds:
        return "Enter at least one seed song (one per line)."

    recommendations = recommend_songs(CATALOG, seeds, int(count))
    if not recommendations:
        return "No recommendations found. Try different seeds or increase the dataset."

    lines = [f"Recommendations for {len(seeds)} seed song(s):", ""]
    for index, rec in enumerate(recommendations, start=1):
        lines.append(f"{index}. {rec.track} — {rec.artist}")
    return "\n".join(lines)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Music Recommender") as demo:
        gr.Markdown(
            """
            # Collaborative Music Recommender

            Enter songs you like (one per line). The system finds listeners with overlapping
            taste and recommends tracks they share.
            """
        )
        seed_box = gr.Textbox(
            label="Seed songs",
            lines=6,
            placeholder="Meet the Frownies\nAmerican Pie\nLollipop | Mika",
        )
        count = gr.Slider(1, 10, value=5, step=1, label="Number of recommendations")
        run = gr.Button("Recommend")
        output = gr.Textbox(label="Results", lines=12)
        run.click(recommend_from_text, inputs=[seed_box, count], outputs=output)
    return demo


def main() -> None:
    build_app().launch()


if __name__ == "__main__":
    main()
