# Cow
_Compose on Webhook_

```bash
docker run --pull --detach \
  --volume "/var/run/docker.sock:/var/run/docker.sock" \
  --volume "/opt/cow/config:/config:ro" \
  --volume "/opt/cow/projects:/config" \
  sirikon/cow
```
