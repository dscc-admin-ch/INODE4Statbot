# File that references the current procedure to create the database

# Deploy psql sevice:
kubectl apply -f cluster.yaml

# Create statbotdb database
PGPASSWORD=password createdb \
  -h postgresql-cnpg-346837-rw \
  -U postgres \
  statbotdb

# Copy database from diffusion folder
mc cp -r s3/jonasmorin/diffusion/statbot_db/statbot.tar.gz

# Go to statbot folder
cd statbot

# Unzip tar file
tar -xvzf statbot.tar.gz

# Restore data into database
sed   -e 's|COPY|\\copy|g'   -e 's|\$\$PATH\$\$/||g' restore.sql | PGPASSWORD=password psql -U postgres postgres
