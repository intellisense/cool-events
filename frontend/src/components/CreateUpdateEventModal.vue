<template>
  <v-dialog
    v-model="show"
    scrollable
    max-width="600px"
  >
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-form
          ref="form"
          lazy-validation
          @submit.prevent="save()"
        >
          <v-text-field
            v-model="editedEvent.title"
            :rules="rules.title"
            :error-messages="getErrors('title')"
            name="title"
            label="Title"
            type="text"
            placeholder="title"
            required
          />
          <v-textarea
            v-model="editedEvent.description"
            :rules="rules.description"
            :error-messages="getErrors('description')"
            name="description"
            label="Description"
            type="description"
            placeholder="description"
            maxlength="500"
            required
            counter
          />
          <date-time-picker
            v-model="editedEvent.start_date"
            :rules="rules.start_date"
            :error-messages="getErrors('start_date')"
            label="Start Date"
            append-icon="mdi-calendar"
            readonly
          />
          <date-time-picker
            v-model="editedEvent.end_date"
            :error-messages="getErrors('end_date')"
            label="End Date"
            required="false"
            append-icon="mdi-calendar"
            readonly
          />
          <NonFieldErrors
            v-if="!saving"
            :errors="getNonFieldErrors()"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <div class="flex-grow-1" />
        <v-btn
          color="blue-grey darken-1"
          text
          @click="show=false"
        >
          Cancel
        </v-btn>
        <v-btn
          color="primary"
          :disabled="saving"
          text
          @click="save"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import eventsAPI from '@/api/events';
import ValidationResponseHandler from '@/mixins/ValidationResponseHandler';
import NonFieldErrors from './NonFieldErrors';
import DateTimePicker from './DateTimePicker';

const defaultEvent = {
  id: null,
  title: '',
  description: '',
  start_date: null,
  end_date: null,
};

export default {
  name: 'CreateUpdateEventModal',
  components: {
    NonFieldErrors,
    DateTimePicker,
  },
  mixins: [ValidationResponseHandler],
  props: {
    visible: {
      type: Boolean,
      required: true,
      default: false,
    },
    eventId: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      saving: false,
      editedEvent: { ...defaultEvent },
      rules: {
        title: [
          (v) => !!v || 'Title is required',
        ],
        description: [
          (v) => !!v || 'Description is required',
        ],
        start_date: [
          (v) => !!v || 'Start date is required',
        ],
      },
    };
  },
  computed: {
    show: {
      get() {
        return this.visible;
      },
      set(value) {
        if (!value) {
          this.$emit('close');
        }
      },
    },
    formTitle() {
      return this.eventId ? 'Update Event' : 'New Event';
    },
  },
  watch: {
    show(currVal, prevVal) {
      if (!currVal && prevVal) {
        this.clearErrors();
        this.$refs.form.reset();
        this.editedEvent = { ...defaultEvent };
      }
      if (currVal && !prevVal) {
        if (this.eventId) {
          this.getEventDetails(this.eventId);
        }
      }
    },
  },
  methods: {
    save() {
      this.clearErrors();
      if (!this.$refs.form.validate()) return;
      this.saving = true;
      this.updateOrCreateEvent()
        .then(({ data }) => {
          this.show = false;
          if (this.eventId) {
            this.$emit('event-updated', data);
          } else {
            this.$emit('event-created', data);
          }
        })
        .catch((error) => this.syncErrors(error))
        .finally(() => {
          this.saving = false;
        });
    },
    updateOrCreateEvent() {
      const payload = { ...this.editedEvent };

      if (this.eventId) {
        return this.updateEvent(payload);
      }

      return this.createEvent(payload);
    },
    updateEvent(payload) {
      return eventsAPI.updateEvent(this.eventId, payload);
    },
    createEvent(payload) {
      return eventsAPI.createEvent(payload);
    },
    getEventDetails(eventId) {
      eventsAPI.getEvent(eventId).then(({ data }) => {
        this.editedEvent = { ...this.editedEvent, ...data };
      });
    },
  },
};
</script>
