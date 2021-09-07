<template>
  <form>
    <div class="modal-card" style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title">Change Password</p>
        <button type="button" class="delete" @click="$emit('close')" />
      </header>
      <section class="modal-card-body">
        <b-field label="New configurator password">
          <b-input
            type="password"
            v-model="newPassword"
            required
            minlength="8"
            maxlength="30"
            password-reveal
          ></b-input>
        </b-field>
        <b-field label="Repeat password" :message="validationText">
          <b-input type="password" v-model="newPasswordRepeat" lazy password-reveal @input="checkInput"></b-input>
        </b-field>
      </section>
      <footer class="modal-card-foot">
        <b-button label="Change Password" type="is-primary" @click="checkAndSend" />
        <b-button label="Close" @click="$emit('close')" />
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  data() {
    return {
      newPassword: "",
      newPasswordRepeat: "",
      validationText: null,
    };
  },
  methods: {
    checkInput() {
      const valid =
        this.newPassword == this.newPasswordRepeat && this.newPassword.length >= 8 && this.newPassword.length <= 30;
      if (valid) {
        this.validationText = null;
      } else {
        this.validationText = "Passwords are not equal.";
      }
      return valid;
    },
    checkAndSend() {
      if (!this.checkInput()) {
        return;
      }
      this.$emit("submit", this.newPassword);
      this.$emit("close");
    },
  },
};
</script>

<style></style>
