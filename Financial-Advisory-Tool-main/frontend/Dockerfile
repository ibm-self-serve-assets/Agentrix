# Stage 1: Build the React app
FROM node:18-alpine AS build

WORKDIR /app

# Install dependencies first (better cache usage)
COPY package*.json ./
RUN npm install

# Copy the rest of the code
COPY . .

# Build the app for production
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:1.21.6-alpine

# Copy built files from previous stage
COPY --from=build /app/build /usr/share/nginx/html

# (Optional) Custom Nginx config
# COPY nginx-custom.conf /etc/nginx/conf.d/default.conf

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]
