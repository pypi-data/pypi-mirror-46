<?php
/**
 * VerveEd setup.
 */

define('CLI_SCRIPT', true);
require(dirname(__FILE__) . '/config.php');
require_once($CFG->libdir . '/testing/generator/data_generator.php');
require_once($CFG->libdir . '/accesslib.php');
require_once($CFG->dirroot . '/webservice/lib.php');
require_once($CFG->dirroot . '/course/externallib.php');

// We don't really need to be admin, except to be able to see the generated tokens
// in the admin settings page, while logged in as admin.
cron_setup_user();

$user = $USER;
$context = context_system::instance();
$manageroleid = $DB->get_field('role', 'id', ['shortname' => 'manager'], MUST_EXIST);
$dg = new testing_data_generator();

// Ensure user is fully set-up.
if (empty($user->email)) {
    $DB->set_field('user', 'email', $user->username . '@example.com', ['id' => $user->id]);
    $USER->email = $user->username . '@example.com';
}

// Create the 'master' course.
core_course_external::create_courses([[
    'fullname' => 'Master course',
    'shortname' => 'master',
    'categoryid' => 1
]]);

// Enable the Web Services.
set_config('enablewebservices', 1);

// Enable Web Services documentation.
set_config('enablewsdocumentation', 1);

// Enable each protocol.
set_config('webserviceprotocols', 'rest');

// Create a role for VerveEd.
if (!$roleid = $DB->get_field('role', 'id', ['shortname' => 'verveed'])) {
    $roleid = $dg->create_role([
        'shortname' => 'verveed',
        'name' => 'VerveEd',
        'description' => '',
        'archetype' => 'editingteacher'
    ]);
}
mtrace('VerveEd role ID: ' . $roleid);

// Create a role for VerveEd Trial.
if (!$roleid = $DB->get_field('role', 'id', ['shortname' => 'verveedtrial'])) {
    $roleid = $dg->create_role([
        'shortname' => 'verveedtrial',
        'name' => 'VerveEd Trial',
        'description' => '',
        'archetype' => 'editingteacher'
    ]);
}
mtrace('VerveEd Trial role ID: ' . $roleid);

// Create a new service with all functions.
$webservicemanager = new webservice();
if (!$service = $DB->get_record('external_services', array('shortname' => 'verveed'))) {
    $service = new stdClass();
    $service->name = 'VerveEd: All functions';
    $service->shortname = 'verveed';
    $service->enabled = 1;
    $service->restrictedusers = 1;
    $service->downloadfiles = 1;
    $service->uploadfiles = 1;
    $service->id = $webservicemanager->add_external_service($service);
}
$functions = $webservicemanager->get_not_associated_external_functions($service->id);
foreach ($functions as $function) {
    $webservicemanager->add_external_function_to_service($function->name, $service->id);
}
if (!$webservicemanager->get_ws_authorised_user($service->id, $user->id)) {
    $adduser = new stdClass();
    $adduser->externalserviceid = $service->id;
    $adduser->userid = $user->id;
    $webservicemanager->add_ws_authorised_user($adduser);
}

// Generate a token for the admin.
if (!$token = $DB->get_field('external_tokens', 'token', ['userid' => $user->id, 'externalserviceid' => $service->id])) {
    $token = external_generate_token(EXTERNAL_TOKEN_PERMANENT, $service->id, $user->id, $context, 0, '');
}
mtrace('Admin token: ' . $token);
