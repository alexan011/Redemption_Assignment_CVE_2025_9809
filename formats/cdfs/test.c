#include <stdio.h>
#include "formats/cdfs.h"

int main(int argc, char **argv)
{
    if (argc < 2) {
        printf("usage: %s <cuefile>\n", argv[0]);
        return 1;
    }

    cdfs_track_t *track = cdfs_open_track(argv[1], 1);

    if (!track) {
        puts("cdfs_open_track() failed");
        return 1;
    }

    puts("Track opened successfully.");

    cdfs_file_t file;
    if (!cdfs_open_file(&file, track, NULL)) {
        puts("cdfs_open_file() failed");
        cdfs_close_track(track);
        return 1;
    }

    puts("File opened successfully.");

    cdfs_close_file(&file);
    cdfs_close_track(track);
    return 0;
}
