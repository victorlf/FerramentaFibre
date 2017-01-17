defProperty('server_node','omf.ufg.node8',"ID of server node")
defProperty('client_node','omf.ufg.node1',"ID of client node")
defProperty('runtime', 60, "Time in second for the experiment is to run")
defProperty('iperf_server_address', '192.168.137.2', "Iperf server IP address")
defProperty('iperf_client_address', '192.168.137.1', "Iperf client IP address")
defProperty('iperf_port', 2000, "Iperf port")
defProperty('iperf_interval', '1', "Iperf interval")
defProperty('iperf_bandwidth', '15M', 'Iperf bandwidth')
defProperty('server_tx_power', '15', 'Server Tx Power')
defProperty('client_tx_power', '15', 'Client Tx Power')
defProperty('bitrate', '54', 'Fixed bitrate value.')

# Define the resources group 'Server'
defGroup('Server', property.server_node) do |node|
  node.addApplication("tutorials:iperf", :id => 'iperf_server') do |app|
    app.setProperty('server', true)
    app.setProperty('port', property.iperf_port)
    app.setProperty('interval', property.iperf_interval)
    app.setProperty('udp', true)
    app.setProperty('reportstyle', 'o')
    app.setProperty('oml-id', 'server')
    app.setProperty('oml-domain', 'wireless_experiment_1')
    app.setProperty('oml-collect', 'tcp:10.137.11.200:3003')
  end

  node.addApplication("tutorials:utils:wlanconfig", :id => 'server_wlanconfig') do |app|
    app.setProperty('wlan', 'wlan0')
    app.setProperty('mode', 'managed')
    app.setProperty('essid', 'omf_pce')
    app.setProperty('tx_power', (property.server_tx_power).to_s)
    app.setProperty('noack', 'true')
    app.setProperty('ip_address', property.iperf_server_address)
    app.setProperty('duration', (property.runtime + 20))
  end

  node.addApplication("tutorials:iwdata", :id => 'iwdata') do |app|
    app.setProperty('wlan', 'wlan0')
    app.setProperty('duration', property.runtime)
    app.setProperty('oml-id', 'server')
    app.setProperty('oml-domain', 'wireless_experiment_1iwdata')
    app.setProperty('oml-collect', 'tcp:10.137.11.200:3003')
  end
end

# Define the resources group 'Client'
defGroup('Client', property.client_node) do |node|
  node.addApplication("tutorials:iperf", :id => 'iperf_client') do |app|
    app.setProperty('client', property.iperf_server_address)
    app.setProperty('port', property.iperf_port)
    app.setProperty('interval', property.iperf_interval)
    app.setProperty('time', property.runtime)
    app.setProperty('udp', true)
    app.setProperty('bandwidth', property.iperf_bandwidth)
    app.setProperty('reportstyle', 'o')
    app.setProperty('oml-id', 'client')
    app.setProperty('oml-domain', 'wireless_experiment_1')
    app.setProperty('oml-collect', 'tcp:10.137.11.200:3003')
  end

  node.addApplication("tutorials:utils:wlanconfig", :id => 'client_wlanconfig') do |app|
    app.setProperty('wlan', 'wlan0')
    app.setProperty('mode', 'master')
    app.setProperty('type', 'a')
    app.setProperty('channel', 48)
    app.setProperty('essid', 'omf_pce')
    app.setProperty('tx_power', (property.client_tx_power).to_s)
    app.setProperty('noack', 'true')
    app.setProperty('bitrate_type', 'fixed')
    app.setProperty('bitrate_value', (property.bitrate).to_s)
    app.setProperty('ip_address', property.iperf_client_address)
    app.setProperty('duration', (property.runtime + 20))
  end
end

onEvent(:ALL_UP_AND_INSTALLED) do |event|
  info "Running tutorial 3: Power control experiment..."
  wait 10
  info "Configuring wireless network between nodes..."
  group("Client").startApplication('client_wlanconfig')
  group("Server").startApplication('server_wlanconfig')
  wait 5
  info "Starting iperf server..."
  group("Server").startApplication('iperf_server')
  wait 5
  info "Starting iperf client..."
  group("Client").startApplication('iperf_client')
  group("Server").startApplication('iwdata')
  info "Iperf server and client started..."
  wait property.runtime
  info "Stopping iperf server and client..."
  wait 5
  allGroups.stopApplications
  info "Iperf server and client stopped..."
  Experiment.done
end
