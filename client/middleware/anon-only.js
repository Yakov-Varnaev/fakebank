export default defineNuxtRouteMiddleware((to, from) => {
  const auth = useAuth();
  const alert = useAlert();
  if (auth.loggedIn) {
    alert.reportInfo("You are already signed in!");
    return navigateTo({ name: "index" });
  }
});
