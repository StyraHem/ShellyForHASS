git tag |
while read in; do
  if [[ $in =~ "test" ]]; then
   echo {$in}
   git tag -d $in
   git push origin :refs/tags/$in
  fi
done
