<template>
  <v-dialog
    v-model="dateTimeDialog"
    :persistent="persistent"
    width="290px"
    @click:outside="closeDialog"
  >
    <template #activator="{ on, attrs }">
      <v-text-field
        :value="dateTimeFormatted"
        readonly
        v-bind="{ ...attrs, ...$attrs }"
        v-on="on"
      />
    </template>
    <v-card class="white">
      <v-toolbar
        height="36"
        color="primary"
        dark
        flat
      >
        <v-tabs
          v-model="tab"
          grow
          height="36"
        >
          <v-tabs-slider color="white" />
          <v-tab href="#date">
            <v-icon>mdi-calendar</v-icon>
          </v-tab>
          <v-tab href="#time">
            <v-icon>mdi-clock</v-icon>
          </v-tab>
        </v-tabs>
      </v-toolbar>

      <v-tabs-items v-model="tab">
        <v-tab-item value="date">
          <v-date-picker
            v-model="date"
            class="rounded-0"
            full-width
            :min="new Date().toISOString().substring(0, 10)"
            @input="tab = 'time'"
          />
        </v-tab-item>
        <v-tab-item value="time">
          <v-time-picker
            :key="tab"
            v-model="time"
            format="ampm"
            class="rounded-0"
            full-width
          />
        </v-tab-item>
      </v-tabs-items>
      <v-card-actions>
        <v-btn
          color="primary"
          @click="closeDialog"
        >
          OK
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import moment from 'moment';

export default {
  name: 'DateTimePicker',
  props: {
    value: {
      type: String,
      default: '',
    },
    persistent: {
      type: Boolean,
      default: false,
    },
    dateFormat: {
      type: String,
      default: 'YYYY-MM-DD',
    },
    timeFormat: {
      type: String,
      default: 'hh:mm',
    },
  },
  data() {
    return {
      date: null,
      time: null,
      tab: false,
      dateTimeDialog: false,
    };
  },
  computed: {
    dateTimeFormatted() {
      return this.$options.filters.formatDateTime(this.value);
    },
  },
  watch: {
    dateTimeDialog: {
      handler(val) {
        // load into separated models as dialog opens
        if (val && this.value) {
          this.date = moment(this.value).format(this.dateFormat);
          this.time = moment(this.value).format(this.timeFormat);
        }
      },
      immediate: true,
    },
  },
  methods: {
    closeDialog() {
      this.dateTimeDialog = false;

      if (this.date && this.time) {
        this.$emit(
          'input',
          moment(`${this.date} ${this.time}`).toDate().toISOString(),
        );
      }

      // prevents animate to date tab when closing
      setTimeout(() => { this.tab = 'date'; }, 300);
    },
  },
};
</script>
