# CodeStory

A tool for drafting the perfect development narratives through commits and PRs.
Craft clear, concise commit messages and PR with ease.

## Idea

- **Miletsotne 1:** the idea is that this will be AI based tool to craft and prepare an accurate git commit messages for code changes have done locally, and prepare a very nice informative and short git commit messages based on semantic commit messages format.
- **Miletsotne 2:** Prepare really nice PR title,  body, that contains a nice and very descrptice PR title, description, label suggestions and other things that are importsnt in PR.
that are based on the local code changes and git comit and commit messages, generate a
- **Miletsotne 3:** user can use our hosted LLM model response or they can also integrate their own local/hosted models as well.

## Task Breakdown

1. Define the user workflow and UI/UX
   - How will users interact with the tool (CLI, VSCode extension, etc)?
   - What are the main features and user flows?

2. Capture local git changes
   - Use a git diff or similar tool to detect file changes
   - Parse diff output to identify files added/modified/deleted

3. Extract code context
   - For modified files, extract surrounding lines of changed code
   - This provides context for the code changes

4. Send data to AI model
   - Package up file changes, context and other metadata
   - Call API or local model to generate commit message

5. Receive and display commit message
   - Return AI-generated commit message from model
   - Allow user to view, edit, accept or reject message

6. Commit to local git repo
   - If accepted, commit changes to local repo with message
   - Integrate with native git workflows

7. Model training (optional)
   - Collect example commit messages mapped to code changes
   - Fine-tune a model (like CLIP) on this data
   - Re-train over time as more data is collected

8. Release iterations
   - Launch with basic CLI or code extension
   - Gather feedback and refine features over time
   - Expand capabilities based on usage

Capturing Local Git Changes - Some ideas:

- Use the `git diff` command to get a diff of changes not yet staged/committed
- Parse the diff output, which lists files changed and the specific lines added/removed
- You can use a Git library for the language (e.g. libgit2 for C/C++) to programmatically get file diffs
- Alternatively, execute `git diff` from code and parse the output

Reading Git References:

- Use `git status` to check the current branch and check for any stashed/untracked changes
- Get the commit SHA of the HEAD to identify latest commit
- For modified files, also get the previous commit SHA to have before/after data

Identifying Changes:

- Compare diff output and commit SHAs to identify exactly what was added/modified/removed
- You'll know the files changed, line numbers, and commit history context

- OR We can read the entire `.git` reference folder and use it as a context

For Model Usage/Fine-Tuning:

- An off-the-shelf model like CLIP could generate initial commit messages
- But fine-tuning on a dataset of code changes and messages may improve results
- Collect examples as users provide feedback, then periodically re-train the model
- Fine-tuning helps the model better understand your project's code and conventions

Resources to train the model :

- <https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716>
- <https://www.conventionalcommits.org/en/v1.0.0/#specification>
- <https://hackwild.com/article/semantic-git-commits/>


<!-- ## Notes for current Hackathon

- Need to use gemini api and other GCP ai services if needed. -->
