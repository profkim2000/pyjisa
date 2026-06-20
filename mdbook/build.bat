cd ..
git pull origin

cd mdbook

mdbook build -d ../docs
copy .\.nojekyll   ..\docs\.nojekyll

cd ..
git add .
git commit -m "update"
git push origin