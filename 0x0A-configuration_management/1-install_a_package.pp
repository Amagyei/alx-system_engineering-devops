#!/usr/bin/pup
# install flask with puppet lint

package  {'flask':
  ensure => installed,
  provider => 'pip3'
}
