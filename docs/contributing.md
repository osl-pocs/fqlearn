# Contributing

```
git checkout main # cambiar a la rama principal
git fetch # actualiza referencias
git pull # jalas los commits 

git checkout -b <nueva-rama>

# Hacer la modificaciones

git add .
git commit -m "mensaje"

git rebase origin/main

# resolver conflictos si existen

git push

# git push origin <nueva rama> # revisar

git push --set-upstream origin nueva
```

This is a document to start contributing

> We are champions

## PR Title Format

```
<tag>(<scope>): <short summary>
  │       │             │
  │       │             └─> Title message. Not capitalized. 
  │       │                 No period at the end.
  │       │
  │       └─> The specific subject of the PR. Can be anything.
  │
  └─> build|chore|ci|docs|feat|fix|perf|refactor|test
```

```py
def factorial():
    pass
```
[link](google.com)

## Tags

|*tag*|*Usage*|
|:---:|:---------:|
|**build**|Changes that affect the build system or external dependencies|
|**chore**|A >minor change and/or daily work activity|
|**ci**|Changes to CI configuration files and scripts|
|**docs**|Documentation only changes|
|**feat**|A new feature|
|**fix**|A bug fix|
|**perf**|A code change that improves performance|
|**refactor**|A code change that neither fixes a bug nor adds a feature|
|**test**|Adding missing tests or correcting existing tests|
|**BREAKING CHANGE**|A code change that breaks the current version|


### The table below shows which commit message gets you which release type when semantic-release runs (using the default configuration):
ref: https://semantic-release.gitbook.io/semantic-release/

|*Commit Message*|*Release Type*|
|:---:|:---------:|
|fix(pencil): stop graphite breaking when too much pressure applied|~~Patch~~ Fix Release|
|feat(pencil): add 'graphiteWidth' option|~~Minor~~ Feature Release|
|BREAKING CHANGE(pencil): remove graphiteWidth option|~~Major~~ Breaking Release|
