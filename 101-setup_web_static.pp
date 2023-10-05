include stdlib

# Update the package lists
exec { 'Update lists':
    command => '/usr/bin/apt update'
}

# Install the web serverNginx
package { 'nginx':
    ensure  => 'present',
    require => Exec['Update lists']
}

# Create the directory tree
exec { 'Create Directory Tree':
    command => '/bin/mkdir -p /data/web_static/releases/test /data/web_static/shared',
    require => Package['nginx']
}

$head = "  <head>\n  </head>"
$body = "  <body>\n    Holberton School\n  </body>"
$index = "<html>\n${head}\n${body}\n</html>\n"

# Create a fake HTML file with some content,
# to test Nginx configuration
file { 'Create Fake HTML':
    ensure  => 'present',
    path    => '/data/web_static/releases/test/index.html',
    content => $index,
    require => Exec['Create Directory Tree']
}

# Create a symbolic link '/data/web_static/current' linked to the
# '/data/web_static/releases/test/' folder.
file { 'Create Symbolic Link':
    ensure  => 'link',
    path    => '/data/web_static/current',
    force   => true,
    target  => '/data/web_static/releases/test',
    require => File['Create Fake HTML']
}

# Ensures that the web server Nginx is running
service { 'nginx':
    ensure  => 'running',
    enable  => true,
    require => Package['nginx']
}

# Set permissions for the 'ubuntu' user
exec { 'Set permissions':
    command => '/bin/chown -R ubuntu:ubuntu /data',
    require => File['Create Symbolic Link']
}

# Set a new location for a Nginx VHost 
$loc_header='location /hbnb_static/ {'
$loc_content='alias /data/web_static/current/;'
$new_location="\n\t${loc_header}\n\t\t${loc_content}\n\t}\n"

# Write the new location to the default Nginx VHost
file_line { 'Set Nginx Location':
    ensure  => 'present',
    path    => '/etc/nginx/sites-available/default',
    after   => 'server_name \_;',
    line    => $new_location,
    notify  => Service['nginx'],
    require => Exec['Set permissions']
}
