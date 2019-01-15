<?php
//require_once("SocketServer.class.php"); // Include the File

error_reporting(E_ALL | E_NOTICE | E_STRICT);
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
//$_SERVER['REMOTE_PORT'];

$address = '192.168.137.1';
$port = 5000;

$failed = 0;

try {
    // Create a socket (AF_INET = IPV4, SOCK_STREAM=TCP stream)
    $failed = 1;
    $sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

    // Bind connection to IP/port
    $failed = 2;
    socket_bind($sock, $address, $port);

    $failed = 3;
    socket_listen($sock, SOMAXCONN);

    while (true) {
        // Accept connection
        $failed = 4;
        $client = socket_accept($sock);

        $failed = 6;
        $rec = socket_read($client, 1024);
        echo $rec;
      }
} catch (Exception $e) {
    if ($failed < 6) {
        $causes = array('create', 'bind', 'listen', 'accept');
        echo 'socket_' . $causes[$failed - 1] . '() failed. Reason: '
                . socket_strerror(socket_last_error($sock)) . '\n';
    } else {
        echo 'Failed at ' . $failed . '\n' . $e . '\n';
    }
  }


/*
while(true) {
//Make sure that it is a POST request.
if(strcasecmp($_SERVER['REQUEST_METHOD'], 'POST') != 0){
    //throw new Exception('Request method must be POST!');
    echo'Request method must be POST!';
}

//Make sure that the content type of the POST request has been set to application/json
$contentType = isset($_SERVER["CONTENT_TYPE"]) ? trim($_SERVER["CONTENT_TYPE"]) : '';
if(strcasecmp($contentType, 'application/json') != 0){
    //throw new Exception('Content type must be: application/json');
    echo 'Content type must be: application/json';
}

//Receive the RAW post data.
$content = trim(file_get_contents("php://input"));

//Attempt to decode the incoming RAW post data from JSON.
$decoded = json_decode($content, true);

//If json_decode failed, the JSON is invalid.
if(!is_array($decoded)){
    //throw new Exception('Received content contained invalid JSON!');
    echo 'Received content contained invalid JSON!';
}
echo 'content';
echo 'decoded';

usleep(100);
}
//Process the JSON.

*/

//$w1 = $_GET["w1"];
//$l1 = $_GET["l1"];
//$t1 = $_GET["t1"];

//$arr = array($w1, $l1, $t1);
// Speichern der Datei
//$sensorData = implode(";", $arr);
//file_put_contents("text.txt", $w1);


/*$addr = '37.97.182.123';
$port = 31351;

$sock = socket_create_listen(0);
socket_getsockname($sock, $addr, $port);
print "Server Listening on $addr:$port\n";
$fp = fopen($port_file, 'w');
fwrite($fp, $port);
fclose($fp);
while($c = socket_accept($sock)) {
   socket_getpeername($c, $raddr, $rport);
   print "Received Connection from $raddr:$rport\n";
}
socket_close($sock);*/

// Set time limit to indefinite execution
  /*  set_time_limit (0);

    // Set the ip and port we will listen on
    $address = '0.0.0.0';
    $port = 23;

    // Create a TCP Stream socket
    $sock = socket_create(AF_INET, SOCK_STREAM, 0);

    // Bind the socket to an address/port
    $bind = socket_bind($sock, $address, $port);

    // Start listening for connections
    socket_listen($sock);

    $client = socket_accept($sock);

    // Read the input from the client &#8211; 1024 bytes
    $input = socket_read($client, 2024);

    // Strip all white spaces from input
    echo $input;

    // Close the master sockets
    $close = socket_close($sock);

    var_dump($close);
*/
/*
$server = new SocketServer("0.0.0.0",1234); // Create a Server binding to the given ip address and listen to port 31337 for connections

$server->max_clients = 10; // Allow no more than 10 people to connect at a time
$server->hook("CONNECT","handle_connect"); // Run handle_connect every time someone connects
$server->hook("INPUT","handle_input"); // Run handle_input whenever text is sent to the server
$server->infinite_loop(); // Run Server Code Until Process is terminated.


function handle_connect(&$server,&$client,$input)
{
    SocketServer::socket_write_smart($client->socket,"String? ","");
}
function handle_input(&$server,&$client,$input)
{
    // You probably want to sanitize your inputs here
    $trim = trim($input); // Trim the input, Remove Line Endings and Extra Whitespace.

    if(strtolower($trim) == "quit") // User Wants to quit the server
    {
        SocketServer::socket_write_smart($client->socket,"Oh... Goodbye..."); // Give the user a sad goodbye message, meany!
        $server->disconnect($client->server_clients_index); // Disconnect this client.
        return; // Ends the function
    }

    $output = $trim; // Reverse the String

    SocketServer::socket_write_smart($client->socket,$output); // Send the Client back the String
    SocketServer::socket_write_smart($client->socket,"String? ",""); // Request Another String
}
*/


/* Allow the script to hang around waiting for connections. */
//set_time_limit(0);

/* Turn on implicit output flushing so we see what we're getting
 * as it comes in. */
//ob_implicit_flush();
/*
$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
echo 'Created socket<br>';

if (!socket_set_option($socket, SOL_SOCKET, SO_REUSEADDR, 1)) {
    echo socket_strerror(socket_last_error($socket));
    exit;
  }

$result = socket_bind($socket, $host, $port) or die("Could not bind to socket!!!!!\n");

$result = socket_listen($socket, 3) or die("Could not set up socket listener\n");
echo 'Listening...';

$spawn = socket_accept($socket) or die("Could not accept incoming connection\n");

$input = socket_read($spawn, 1024) or die("Could not read input\n");

echo $input;

*/
?>
