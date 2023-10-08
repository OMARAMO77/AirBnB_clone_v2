# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file { '/data/web_static':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  content => '<html>
                <head>
                </head>
                <body>
                  Holberton School
                </body>
              </html>',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => "server {
                listen 80 default_server;
                listen [::]:80 default_server;

                server_name _;

                location /hbnb_static {
                    alias /data/web_static/current;
                }
                # Other configurations...
            }",
  notify  => Service['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
