export default defineNuxtRouteMiddleware((to, from) => {
  const auth = useAuth();
  const alert = useAlert();
  if (!auth.loggedIn) {
    alert.reportInfo("Please sign in!");
    return navigateTo({ name: "signin" });
  }
});
