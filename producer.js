const kafka = require('kafka-node');

const client = new kafka.KafkaClient({ kafkaHost: 'localhost:9093' }); // Changed from 9092 to 9093
const producer = new kafka.Producer(client);

const endpoints = ['/users', '/products', '/checkout', '/login', '/orders', '/cart', '/payments', '/reviews', '/profile', '/search'];
const statuses = ['success', 'error'];
const errorTypes = [null, '404 Not Found', '500 Internal Server Error', '402 Payment Required', '503 Service Unavailable'];

function generateLog() {
  const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  const status = statuses[Math.floor(Math.random() * statuses.length)];
  const errorType = status === 'error' ? errorTypes[Math.floor(Math.random() * errorTypes.length)] : null;
  const responseTime = Math.floor(Math.random() * 400) + 100;

  return {
    topic: 'logs',
    messages: JSON.stringify({
      endpoint,
      status,
      response_time: responseTime,
      error_type: errorType,
      timestamp: new Date().toISOString()
    })
  };
}

producer.on('ready', () => {
  console.log('Producer is ready...');
  setInterval(() => {
    const payload = [generateLog()];
    producer.send(payload, (err, data) => {
      if (err) {
        console.error('Error sending message:', err);
      } else {
        console.log('Message sent successfully:', data);
      }
    });
  }, 2000); // Send every 2 seconds
});

producer.on('error', (err) => {
  console.error('Producer error:', err);
});