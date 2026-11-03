import argparse
import json
import random


def clean_title(title):
    return title.replace("\t", " ").replace("\n", " ").replace("\r", " ")


def load_posts(json_path):
    with open(json_path, encoding="utf-8") as f:
        payload = json.load(f)

    children = payload["data"]["children"]

    posts = []
    for child in children:
        data = child.get("data", {})
        name = data.get("name")
        title = data.get("title")
        if name is None or title is None:
            continue
        posts.append({"name": name, "title": clean_title(title)})
    return posts


def sample_posts(posts, n, seed):
    if n >= len(posts):
        return posts
    rng = random.Random(seed)
    return rng.sample(posts, n)


def write_tsv(posts, out_path):
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("Name\ttitle\tcoding\n")
        for post in posts:
            f.write(f"{post['name']}\t\"{post['title']}\"\t\n")


def main():
    parser = argparse.ArgumentParser(
        description="Sample Reddit posts from a listing JSON into a TSV."
    )
    parser.add_argument(
        "-o",
        dest="out_file",
        required=True,
        help="Output TSV path",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional RNG seed for reproducible sampling",
    )
    parser.add_argument("json_file", help="Reddit listing JSON file")
    parser.add_argument(
        "num_posts_to_output",
        type=int,
        help="Number of posts to randomly sample",
    )
    args = parser.parse_args()

    posts = load_posts(args.json_file)
    selected = sample_posts(posts, args.num_posts_to_output, args.seed)
    write_tsv(selected, args.out_file)


if __name__ == "__main__":
    main()
