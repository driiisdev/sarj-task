const baseUrl = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '/api/v1') || 'https://sarj-task.onrender.com/api/v1';

export default baseUrl;
