#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

import git


def camp(commit_message: Optional[str] = None) -> None:
    """Add and commit changes made to tracked files, then push the commit.

    :param message: The commit message to be passed to the git commit command.
    :note: A commit message will be automatically generated
           if the ``message`` argument is not provided.
    """
    repo = git.Repo(search_parent_directories=True)

    changed_file_lists = [
        [file.a_path
         for file in repo.index.diff(None).iter_change_type(change_type)]
        for change_type in ('D', 'M')
    ]

    if any(changed_file_lists):

        prefixes = "Deleted files:", "Modified files:"

        deleted, modified = (
            f"{prefix} {', '.join(changed)}. " if changed else ""
            for prefix, changed in zip(prefixes, changed_file_lists)
        )

        print("Adding deleted and modified files.",
              repo.git.add("--update"))

        if commit_message:
            print(repo.git.commit(changed_file_lists,
                                  message=commit_message),
                  repo.git.push(),
                  f"\nPushing to {', '.join(repo.remote().urls)}.")

        else:

            print(repo.git.commit(changed_file_lists,
                                  message=deleted + modified),
                  repo.git.push(),
                  f"\nPushing to {', '.join(repo.remote().urls)}.")

    else:
        print("There are no deleted or modified files.")


if __name__ == "__main__":
    camp()
