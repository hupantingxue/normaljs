/*
 * echo.c --
 *
 *	Produce a page containing all FastCGI inputs
 *
 *
 * Copyright (c) 1996 Open Market, Inc.
 *
 * See the file "LICENSE.TERMS" for information on usage and redistribution
 * of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 *
 */
#ifndef lint
static const char rcsid[] = "$Id: echo.c,v 1.5 1999/07/28 00:29:37 roberts Exp $";
#endif /* not lint */

#include "fcgi_config.h"

#include <stdlib.h>
#include <string.h>

#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif

#ifdef _WIN32
#include <process.h>
#else
extern char **environ;
#endif

#include <iostream>
#include "fcgi_stdio.h"
#include "cgi.h"


static void PrintHeader()
{
    printf("Content-type: text/html\r\n\r\n");
}

static void SndRsp(int rspCode, char *szMsg)
{
    PrintHeader();
    printf("{\"errcode\":%d,\"errmsg\":%s}", rspCode, szMsg);
}

int main ()
{
    char **initialEnv = environ;
    int count = 0;
    char *testStr = NULL;

    char *xqID = NULL;
    char errmsg[1024] = {0};
    int errcode = 0;

    while (FCGI_Accept() >= 0) {
        char *queryStr= getenv("QUERY_STRING");
        int len;

        len = strlen(queryStr);
        memset(errmsg, 0, sizeof(errmsg));

        if ((NULL == queryStr) || (0 >= len))
        {
            errcode = 1002;
            snprintf(errmsg, sizeof(errmsg), "{Paramater error.}");
        }
        else
        {
            xqID = Cgi_Value("xqid");
        }
        
        errcode = 200;        
        // snprintf(errmsg, sizeof(errmsg), "[{\"id\": 1,\"url\": \"http://baidu.com\",\"tel\": \"0755-88888888\",\"desc\": \"市民中心\",\"purl\": \"http://baidu.com\",\"salecnt\": 10,\"price\": 10},{\"id\": 2,\"url\": \"http://baidu.com\",\"tel\": \"0755-66666666\",\"desc\": \"天地间\",\"purl\": \"http://baidu.com\",\"salecnt\": 10,\"price\": 10}]");
        snprintf(errmsg, sizeof(errmsg), "[{\"id\": 1,\"url\": \"http://m.dianping.com/shop/2377219\",\"tel\": \"0755-86359922\",\"name\":\"四海一家\",\"desc\": \"文心五路33号海岸城广场513，近保利广场\",\"purl\": \"http://211.154.149.170:8099/pic/tg/1.jpg\",\"salecnt\": 10,\"price\": 133}, {\"id\": 2,\"url\": \"http://shop71812442.taobao.com\",\"name\":\"百味云享\",\"desc\": \"进口食品年货提前抢购\",\"purl\": \"http://211.154.149.170:8099/pic/tg/2.jpg\",\"salecnt\": 28,\"price\": 99}]");        SndRsp(errcode, errmsg);
    } /* while */

    return 0;
}
