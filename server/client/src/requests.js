import axios from 'axios';

const url = 'http://localhost:80';

const authRequest = () => {
  const defaultOptions = {
    baseURL: url,
    timeout: 1000 * 30,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // Create instance
  const instance = axios.create(defaultOptions);

  // Set the AUTH token for any request
  /* eslint-disable no-param-reassign */
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    config.headers.Authorization = token ? `Token ${token}` : '';

    return config;
  });
  /* eslint-enable no-param-reassign */
  return instance;
};

export default authRequest();
