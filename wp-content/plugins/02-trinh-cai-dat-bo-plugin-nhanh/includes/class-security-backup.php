<?php
/**
 * WP Security Shield - Module Bảo Lưu & Khôi Phục Dữ Liệu
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_Security_Shield_Backup {

    private $backup_dir;

    public function __construct() {
        $upload = wp_upload_dir();
        $this->backup_dir = $upload['basedir'] . '/wp-security-shield-backups/';
        $this->init_backup_dir();
    }

    private function init_backup_dir() {
        if ( ! file_exists( $this->backup_dir ) ) {
            wp_mkdir_p( $this->backup_dir );
            @file_put_contents( $this->backup_dir . '.htaccess', "Deny from all\n" );
            @file_put_contents( $this->backup_dir . 'index.php', "<?php // Silence is golden." );
        }
    }

    public function create_backup( $opts = array() ) {
        $time_stamp = date( 'Y-m-d_H-i-s' );
        $backup_id = 'backup_' . $time_stamp;

        $include_db = ! empty( $opts['db'] );
        $include_config = ! empty( $opts['config'] );
        $include_snapshot = ! empty( $opts['snapshot'] );

        $files_created = array();

        if ( $include_db ) {
            $db_file = $this->export_database( $backup_id );
            if ( $db_file ) {
                $files_created['db'] = $db_file;
            }
        }

        if ( $include_config ) {
            $config_files = $this->backup_configs( $backup_id );
            if ( ! empty( $config_files ) ) {
                $files_created['configs'] = $config_files;
            }
        }

        if ( $include_snapshot ) {
            $snapshot_file = $this->create_snapshot( $backup_id );
            if ( $snapshot_file ) {
                $files_created['snapshot'] = $snapshot_file;
            }
        }

        $backups = get_option( 'wp_security_shield_backups_list', array() );
        $backups[$backup_id] = array(
            'id'          => $backup_id,
            'created_at'  => date( 'Y-m-d H:i:s' ),
            'files'       => $files_created,
            'options'     => $opts
        );

        update_option( 'wp_security_shield_backups_list', $backups );

        return array( 'success' => true, 'backup_id' => $backup_id );
    }

    private function export_database( $backup_id ) {
        global $wpdb;
        $tables = $wpdb->get_col( "SHOW TABLES" );
        
        $sql = "-- WP Security Shield DB Backup\n";
        $sql .= "-- Generation Time: " . date( 'Y-m-d H:i:s' ) . "\n\n";

        foreach ( $tables as $table ) {
            $create = $wpdb->get_row( "SHOW CREATE TABLE {$table}", ARRAY_N );
            $sql .= "\n\n" . $create[1] . ";\n\n";

            $rows = $wpdb->get_results( "SELECT * FROM {$table}", ARRAY_A );
            if ( ! empty( $rows ) ) {
                foreach ( $rows as $row ) {
                    $keys = array_keys( $row );
                    $vals = array_values( $row );

                    $escaped_vals = array_map( function( $v ) use ( $wpdb ) {
                        if ( is_null( $v ) ) return "NULL";
                        return "'" . esc_sql( $v ) . "'";
                    }, $vals );

                    $sql .= "INSERT INTO {$table} (`" . implode( "`, `", $keys ) . "`) VALUES (" . implode( ", ", $escaped_vals ) . ");\n";
                }
            }
        }

        $filename = $this->backup_dir . $backup_id . '_db.sql';
        @file_put_contents( $filename, $sql );
        return file_exists( $filename ) ? $filename : false;
    }

    private function backup_configs( $backup_id ) {
        $saved = array();
        $config_path = ABSPATH . 'wp-config.php';
        $htaccess_path = ABSPATH . '.htaccess';

        if ( file_exists( $config_path ) ) {
            $dest = $this->backup_dir . $backup_id . '_wp-config.php';
            @copy( $config_path, $dest );
            if ( file_exists( $dest ) ) $saved['wp-config'] = $dest;
        }

        if ( file_exists( $htaccess_path ) ) {
            $dest = $this->backup_dir . $backup_id . '_.htaccess';
            @copy( $htaccess_path, $dest );
            if ( file_exists( $dest ) ) $saved['htaccess'] = $dest;
        }

        return $saved;
    }

    private function create_snapshot( $backup_id ) {
        $upload_dir = wp_upload_dir();
        $target_path = $upload_dir['basedir'];

        $snapshot = array();
        if ( is_dir( $target_path ) ) {
            $dir_iter = new RecursiveDirectoryIterator( $target_path, RecursiveDirectoryIterator::SKIP_DOTS );
            $iter = new RecursiveIteratorIterator( $dir_iter );

            foreach ( $iter as $file ) {
                if ( $file->isFile() ) {
                    $rel = str_replace( wp_normalize_path( ABSPATH ), '', wp_normalize_path( $file->getPathname() ) );
                    $snapshot[$rel] = array(
                        'size' => $file->getSize(),
                        'mtime' => $file->getMTime(),
                        'md5'   => md5_file( $file->getPathname() )
                    );
                }
            }
        }

        $filename = $this->backup_dir . $backup_id . '_snapshot.json';
        @file_put_contents( $filename, wp_json_encode( $snapshot ) );
        return file_exists( $filename ) ? $filename : false;
    }
}
