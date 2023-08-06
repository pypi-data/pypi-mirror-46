Stormbot role plugin
====================

This is a Stormbot_ plugin that let user volunteer for some roles. And then
assign those role randomly for a given duration::

    <master>   | stormbot: whois Scrum-Master
    <stormbot> | nobody is willing to be Scrum-Master

    <master>   | stormbot: whocouldbe Scrum-Master
    <stormbot> | nobody is volunteer to be Scrum-Master

    <master>   | stormbot: icouldbe Scrum-Master
    <stormbot> | master: glad to here that
    <stormbot> | master is volunteer for Scrum-Master

    <michel>   | stormbot: icouldbe Scrum-Master
    <stormbot> | master: glad to here that
    <stormbot> | master, michel are volunteers for Scrum-Master

    <master>   | stormbot: iam Scrum-Master
    <stormbot> | master: thanks!
    <stormbot> | master is Scrum-Master for 5 days, 13:32:48.239574

    <michel>   | Scrum-Master: could you help me?
    <stormbot> | master: Scrum-Master: could you help me ?

    <master>   | stormbot: sit-out Scrum-Master
    <stormbot> | master: coward!
    <stormbot> | michel: you are now Scrum-Master thanks to master's cowardice

    <master>   | stormbot: icantbe Scrum-Master
    <stormbot> | master: sad news…
    <stormbot> | michel is volunteer to be Scrum-Master

.. _Stormbot: https://pypi.org/project/stormbot

Example
=======

::

    stormbot --plugins stormbot_role.role --role Scrum-Master --role-start 2017-05-29T00 --role-duration P1W

License
=======

::

    Permission to use, copy, modify, and distribute this software for any
    purpose with or without fee is hereby granted, provided that the above
    copyright notice and this permission notice appear in all copies.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
