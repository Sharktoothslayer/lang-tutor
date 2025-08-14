# Use nginx directly with pre-built files
FROM nginx:alpine

# Copy the pre-built HTML file
COPY build/index.html /usr/share/nginx/html/index.html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 