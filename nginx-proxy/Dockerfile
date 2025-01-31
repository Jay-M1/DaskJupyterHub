FROM centos:7.6.1810

# Install some packages
RUN yum -y --nogpg install epel-release && yum clean all
RUN yum -y --nogpg install nginx && yum clean all

# Configure nginx
ADD nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80
EXPOSE 443

# Command executed when container started
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
