# ToDo

**Note**: This information is given any time there is an invalid
input, and is also stored in `help`. `help` will be more up to date
because it is the file printed with invalid inputs.

This is a script to update the to-do list in various ways. 
It is run only with flags and user inputs. The general 
form is as follows:

  python3 modify.py [-flags] <card#> [args]

The available flags are the following:

  -b <card#>
    Blocks card <card#>.

  -c <card#> 
    Creates a card with the number <card#> of type <type>, 
    where the type is determined in the script with a user
    input. Also sets up the link to Kanbanize, a template 
    notes card that tells you to make a real one, and an 
    invalid PR link.

  -d <card#>
    Deletes the link to the notes for card <card#> if the 
    link is to the template file. You probably don't want 
    to use this because it makes it more work to add notes 
    to the card, and it's bundled with -r anyway.

  -n <card#>
    Adds a file for the notes for a card, and links to it 
    on the entry for that card on the "In Progess" page.

  -p <card#> 
    Changes the PR link to a valid one (assuming you 
    haven't already done this) by adding the PR number to 
    the link. The PR number is asked for as a user input
    during the script. This only does something if there's 
    a GitHub PR link in the card.

  -q <card#>
    Moves a card to QA. **This is currently obsolete, but 
    may be readded later.**

  -r <card#>
    Archives a card by removing it from the "In Progress" 
    page and adding it to the corresponding archive page. 
    Also updates the links for the card and its colour on 
    the card list. If there is a notes page, the link is
    updated, and if not the dead link is deleted from the 
    card on the archive page.

  -t 
    Can be combined with any flag to test it. All the 
    changed files are link on the test output page, 
    which can be accessed from the card list page.

  -u 
    Used to update the file config to rearrange the 
    structure of the files in the archive. To do the 
    update, put the new config files in the update
    directory and run this script. The config will be 
    updated (assuming the test flag is not set). If 
    updating the partitioning of the cards, the old 
    files will be written to the directory "archiveOld" 
    before they are overwritten to avoid the loss of data. 
    If you want you can delete that directory after the 
    script is run.

  -v 
    Used to clean all the test directories, along with 
    bugsTest.md and archiveTest.md.

  -z <card#>
    Unblocks card <card#>.

At the moment, flags cannot be combined (except for the testing flag).
