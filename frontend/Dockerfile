# Stage 1: Build the React application
FROM node:16-alpine as build

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:1.21.3-alpine

# Copy the build output to replace the default Nginx contents.
COPY --from=build /app/build /usr/share/nginx/html

# Copy a custom Nginx configuration
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 