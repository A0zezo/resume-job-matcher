"""Rank job descriptions against your resume.

Usage: python -m matcher.cli resume.txt jobs/*.txt [--top 5]
"""

import argparse
import glob
import os

from .core import rank_jobs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="resume file followed by job description files (globs ok)")
    parser.add_argument("--top", type=int, default=None)
    args = parser.parse_args()

    paths = []
    for pattern in args.inputs:
        paths.extend(sorted(glob.glob(pattern)))
    if len(paths) < 2:
        parser.error("need a resume file and at least one job description file")

    with open(paths[0], encoding="utf-8") as f:
        resume = f.read()
    jobs = {}
    for path in paths[1:]:
        with open(path, encoding="utf-8") as f:
            jobs[os.path.splitext(os.path.basename(path))[0]] = f.read()

    for i, match in enumerate(rank_jobs(resume, jobs, top_k=args.top), 1):
        print(f"\n#{i}  {match.job}  (similarity {match.score:.3f})")
        print(f"    matched skills : {', '.join(match.matched_skills) or '-'}")
        print(f"    missing skills : {', '.join(match.missing_skills) or '-'}")


if __name__ == "__main__":
    main()
