# install flask with puppet lint

package  {'python3-pip':
  ensure => installed,
}

exec {'install_flask':
  command => '/usr/bin/pip3 insall flask==2.1.0',
  unless  => '/usr/bin/pip3 show flask | grep -q "Version: 2.1.0"',
  require => Package['python3-pip'],
} 
