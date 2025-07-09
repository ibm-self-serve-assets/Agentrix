# # Step 1: Build the React app
# FROM node:18-alpine AS build
# # 

# # Set the working directory
# WORKDIR /app

# # Install dependencies
# COPY package.json package-lock.json ./
# RUN npm cache clean --force
# # RUN npm install --verbose
# RUN npm install

# # Copy the source files
# COPY . .

# # Build the React app
# RUN npm run build

# # Expose port 80
# EXPOSE 8080

# # Start Nginx
# CMD ["npm", "run", "preview"]
# Use Nginx to serve the pre-built Vite app
FROM nginx:alpine

# Set working directory to Nginx's HTML directory
WORKDIR /usr/share/nginx/html

# Remove default Nginx static files
RUN rm -rf ./*

# Copy Vite build output (dist/) into Nginx HTML folder
COPY dist/ .

# Optional: Custom Nginx config (recommended for SPAs)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose default port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]