echo "Enter the Migration File name"
read name
alembic revision --autogenerate -m "$name"
echo "Migration File Created. Don't Forget to Commit it"