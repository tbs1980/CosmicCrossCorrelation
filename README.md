# Cosmic-Cross-Correlation

>A project to measure cross-correlations between various cosmological data

## Contributors

* Filipe Abdalla (fba@star.ucl.ac.uk)
* Sree Balan (sbalan@star.ucl.ac.uk)
* Aurelien Benoit-Levy (aurelien.benoit-levy@ucl.ac.uk)
* Stephanie Jouvel (sjouvel@star.ucl.ac.uk)
* Donnacha Kirk (drgk@star.ucl.ac.uk)
* Ofer Lahav (o.lahav@ucl.ac.uk)
* Marc Manera (manera.work@gmail.com)
* Michael McLeod (mmcleod@star.ucl.ac.uk)
* Bruno Moraes (moraes@star.ucl.ac.uk)

## Guidelines for adding contents

It is better if you keep a local copy of this repository in you machine. You can do this cloning the repository ( I assume that you have `git` installed in your computer.)

	$ git clone https://github.com/tbs1980/CosmicCrossCorrelation.git

This will create a directory with all the files from the repository. BEFORE YOU MAKE ANY CHANGES TO THE CONTENTS, please create a new local branch so that all changes you make are logged properly in this branch and thus does make things easier for others to contribute simultaneoursly. You can make a new branch (let's call this `sree_testing_layout`) by

	$ cd CosmicCrossCorrelation
	$ git branch sree_testing_layout

You can see all the branches insided the repository by typing

	$ git branch
	* master
	  sree_testing_layout

The star on master indicates that you are currently in `master` branch. Move to your barch by checking out that branch.

	$ git checkout sree_testing_layout
	Switched to branch 'sree_testing_layout'

Now you are ready to make changes to the repository. At any time you may check the status of the repository by using the `git status` command. You will see something like below

	$ git status
	On branch sree_testing_layout
	Changes not staged for commit:
	  (use "git add <file>..." to update what will be committed)
	  (use "git checkout -- <file>..." to discard changes in working directory)

		modified:   .gitignore
		modified:   README.md

	Untracked files:
	  (use "git add <file>..." to include in what will be committed)

		doc/
		minutes/

	no changes added to commit (use "git add" and/or "git commit -a")

If are ready to add these changes to the repo you can do that by the commands `git add` and `git commit`.

	$ git add .
	$ git status
	On branch sree_testing_layout
	Changes to be committed:
	  (use "git reset HEAD <file>..." to unstage)

		modified:   .gitignore
		modified:   README.md
		new file:   doc/README.md
		new file:   minutes/2014_07_04.md

As you can see git has listed the files that were modified. Now you can commit these changes to the repo. Please note that I add a detailed commit message so that we get a detailed log of what is happening.

	$ git commit -m "First commit to my branch. Added minutes directorya and mintes from 7th July. Also added a doc directory to hold the documentation. "
	[sree_testing_layout 1a07e22] First commit to my branch. Added minutes directorya and mintes from 7th July. Also added a doc directory to hold the documentation.
	 4 files changed, 100 insertions(+), 4 deletions(-)
	 rewrite README.md (99%)
	 create mode 100644 doc/README.md
	 create mode 100644 minutes/2014_07_04.md

Now push these changes to the github repository so that everyone has access to the changes you made.

	$ git push --set-upstream origin sree_testing_layout





