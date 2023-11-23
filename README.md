# Cow
_Compose on Webhook_

```bash
docker run --pull always --detach \
  --volume "/var/run/docker.sock:/var/run/docker.sock" \
  --volume "/opt/cow/config:/config:ro" \
  --volume "/opt/cow/projects:/projects" \
  --publish 127.0.0.1:40000:80 \
  sirikon/cow
```
