git tag -d latest
git push origin :refs/tags/latest
git tag -a latest -m"latest"
git push --tags -f
