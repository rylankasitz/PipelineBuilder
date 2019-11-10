relpath="./pipelines/"$1
path=$(realpath $relpath)

export PATH="$path:$PATH"

echo "Run sbatch "$1".sh with correct parameters you specify!"