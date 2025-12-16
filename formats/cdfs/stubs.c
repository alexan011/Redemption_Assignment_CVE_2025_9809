#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include <streams/interface_stream.h>

/* -------------------------------------------------------
   Define our own backend storage for intfstream_internal_t
   ------------------------------------------------------- */

struct intfstream_internal {
    FILE *fp;
};

typedef struct intfstream_internal intfstream_internal_t;

/* -------------------------------------------------------
   Minimal backend implementation
   ------------------------------------------------------- */

intfstream_internal_t *intfstream_open_file(const char *path,
                                            unsigned access,
                                            unsigned hint)
{
    (void)access;
    (void)hint;

    FILE *fp = fopen(path, "rb");
    if (!fp)
        return NULL;

    intfstream_internal_t *s = malloc(sizeof(*s));
    s->fp = fp;
    return s;
}

int64_t intfstream_get_size(intfstream_internal_t *s)
{
    long pos = ftell(s->fp);
    fseek(s->fp, 0, SEEK_END);
    long size = ftell(s->fp);
    fseek(s->fp, pos, SEEK_SET);
    return size;
}

int64_t intfstream_read(intfstream_internal_t *s, void *buf, uint64_t len)
{
    return fread(buf, 1, len, s->fp);
}

int64_t intfstream_seek(intfstream_internal_t *s, int64_t offset, int whence)
{
    return fseek(s->fp, offset, whence);
}

int intfstream_close(intfstream_internal_t *s)
{
    if (!s) return 0;
    fclose(s->fp);
    free(s);
    return 0;
}

uint32_t intfstream_get_frame_size(intfstream_internal_t *s)
{
    (void)s;
    return 2352;
}

uint32_t intfstream_get_offset_to_start(intfstream_internal_t *s)
{
    (void)s;
    return 0;
}

uint32_t intfstream_get_first_sector(intfstream_internal_t *s)
{
    (void)s;
    return 0;
}

/* CHD tracks not used */
intfstream_internal_t *intfstream_open_chd_track(const char *path,
                                                 unsigned access,
                                                 unsigned hint,
                                                 int track)
{
    (void)path; (void)access; (void)hint; (void)track;
    return NULL;
}
