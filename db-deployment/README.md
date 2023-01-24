This creates a deployment for the database. 
Because we use an embedded helm chart for the database this is only here to demonstrate that we know how to do it ourselves.


Execute:
```bash
# To install the database
./run.sh --install


# To fill some data in the database
./run.sh --fill

# To see the filled data
./run.sh --test

# To restart the deployment
./run.sh --restart-deployment

# View if the data in the db is still the same
./run.sh --test
```