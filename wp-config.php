<?php//Begin Really Simple Security key
define('RSSSL_KEY', 'L65Mz66bsmnAY2pMMWaJPOaOpIsfl73K061LKUkCxvPtSmfbCnkWYTYCyz4mE19Q');
//END Really Simple Security key

/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the website, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://developer.wordpress.org/advanced-administration/wordpress/wp-config/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'demo1220_englishchitra' );

/** Database username */
define( 'DB_USER', 'demo1220_englishchitra' );

/** Database password */
define( 'DB_PASSWORD', 'G_uT[7v(?;s@@(bU' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'V hkH7gwqGzmWBhyQ/G;6c`e03^<0/9SAPMa|J3]KaE?Y#As?eU*_?s~p)o7KJD ' );
define( 'SECURE_AUTH_KEY',  'OU7@wu<:U.b<l7BFh3tM=aG*zvOF*d$<5XRaoj+)^8<AaTwu,e)eQ)AVrtsr16/U' );
define( 'LOGGED_IN_KEY',    ']PS3!S_ Aa#~X5X=c~EUExN!=.U yBq?[8vX9A6pYSm2z-Sl%jOSRzEA+lihmi5<' );
define( 'NONCE_KEY',        '*FB0Han;K{HX{QaF<5!H!Nh[*h=LZ^,^;H3j.M+;L.42=c3f6oAzCqnq?7$Dci.!' );
define( 'AUTH_SALT',        'TOqK]0@LOty[!.R.FZMma>6F^$[Vi2W2peL2u8&;2dIb=8?)a>xWPk$E7bS`GS7v' );
define( 'SECURE_AUTH_SALT', '&~W3U596}o>sT&{;tRDq?7FuevtB9D6RQk^^.-h#oXm$&mVUd+A%y:Z:fNEa{&5C' );
define( 'LOGGED_IN_SALT',   'H*cJtU>=4InzA,X= |REm1 B&&owOj8adrr;ND@^pz})kjp#aMWo7?iklIUS8[2Q' );
define( 'NONCE_SALT',       'i/R{gV>5bVU[S8a59!<O3@x%EQX${%;5cY!k]{UdC:<$Sb?6FNRpp3u~]W-AE[l+' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 *
 * At the installation time, database tables are created with the specified prefix.
 * Changing this value after WordPress is installed will make your site think
 * it has not been installed.
 *
 * @link https://developer.wordpress.org/advanced-administration/wordpress/wp-config/#table-prefix
 */
$table_prefix = 'wpz_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
