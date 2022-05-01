import session from './session';

export default {
  login(email, password) {
    return session.post('/login/', { email, password });
  },
  logout() {
    return session.post('/logout/', {});
  },
  signup(email, password1, password2) {
    return session.post('/signup/', { email, password1, password2 });
  },
  getUserDetails() {
    return session.get('/user/');
  },
};
