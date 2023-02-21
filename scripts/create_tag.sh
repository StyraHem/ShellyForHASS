if [ $1 == '' ]
then
  echo Param1 lika 1.0.0.beta.1
fi
git tag -a $1 -m $1
git push --tags
