---
title: Note 210545474
published: Thu, 05 Feb 2026 23:32:03 GMT
author: Cengiz Han
handle: hancengiz
url: https://substack.com/note/c-210545474
type: note
note_id: 210545474
photo_url: https://substackcdn.com/image/fetch/$s_!A8_F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd3c9352-78f7-4a7e-ab29-7efd239dd41c_400x400.jpeg
reactions: 0
restacks: 0
replies: 0
---
1M context window was not supposed to not be available in claude code. it is documented to be in the api and agents sdk. 

apperantly this works. /model opus\[1m\] (hope it does not try to compact 200k, since 1M context wid might not be ofically supported yet)

![Image](image1.png)
