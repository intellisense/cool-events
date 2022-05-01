const ValidationResponseHandler = {
  data() {
    return {
      errors: {},
    };
  },
  methods: {
    syncErrors(error) {
      if (typeof error !== 'undefined') {
        if (typeof error.response !== 'undefined'
          && Object.prototype.hasOwnProperty.call(error, 'response')
          && Object.prototype.hasOwnProperty.call(error.response, 'data')
        ) {
          this.errors = error.response.data;
        }
      }
    },
    clearErrors() {
      this.$set(this.$data, 'errors', {});
    },
    hasErrors(field) {
      return Object.prototype.hasOwnProperty.call(this.errors, field);
    },
    getError(field) {
      return Object.prototype.hasOwnProperty.call(this.errors, field)
        ? this.errors[field][0] : null;
    },
    getErrors(field) {
      return Object.prototype.hasOwnProperty.call(this.errors, field)
        ? this.errors[field] : [];
    },
    getNonFieldErrors() {
      const key = 'non_field_errors';
      return Object.prototype.hasOwnProperty.call(this.errors, key)
        ? this.errors[key] : [];
    },
  },
};

export default ValidationResponseHandler;
