import pusher

client = pusher.Pusher(
    app_id = "1706778",
    key = "7ccf4bc1ee9c8d02d536",
    secret = "e7663f8d9b97f6442b07",
    cluster = "eu"
)

client.trigger(u'my-channel', u'my-event', {u'message': u'hello world'})