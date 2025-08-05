import { Calendar, HelpCircle, Home, Inbox, Search, User } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { NavUser } from "./mine/nav-user"
import { useAuth } from "@/hooks/use-auth"
import { useRouter } from "@/hooks/use-router"
import { useTranslation } from "@/lib/i18n"

export function AppSidebar() {
  const { user, isAuthenticated } = useAuth()
  const { navigate, currentRoute } = useRouter()
  const { t } = useTranslation(user?.language)

  // Menu items con traduzioni
  const items = [
    {
      title: t("home"),
      route: 'home' as const,
      icon: Home,
    },
    {
      title: t("inbox"),
      route: 'home' as const, // placeholder
      icon: Inbox,
    },
    {
      title: t("calendar"),
      route: 'home' as const, // placeholder
      icon: Calendar,
    },
    {
      title: t("search"),
      route: 'home' as const, // placeholder
      icon: Search,
    },
  ]

  const navSecondary = [
    {
      title: t("profile"),
      route: 'profile' as const,
      icon: User,
    },
    {
      title: t("getHelp"),
      route: 'home' as const, // placeholder
      icon: HelpCircle,
    },
  ]

  const handleNavigation = (route: 'home' | 'profile') => {
    console.log('Sidebar: Button clicked, navigating to:', route)
    navigate(route)
    console.log('Sidebar: Navigate function called')
  }

  // Se l'utente non è autenticato, mostra dati di default
  const displayUser = isAuthenticated && user ? {
    name: `${user.first_name} ${user.last_name}`,
    email: user.email,
    avatar: user.profile_picture ? `data:image/jpeg;base64,${user.profile_picture}` : `https://api.dicebear.com/7.x/initials/svg?seed=${user.first_name}%20${user.last_name}`,
  } : {
    name: t("guestUser"),
    email: "guest@example.com", 
    avatar: "https://api.dicebear.com/7.x/initials/svg?seed=Guest%20User",
  }

  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>{t("application")}</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    onClick={() => handleNavigation(item.route)}
                    isActive={currentRoute === item.route}
                    className="cursor-pointer"
                  >
                    <item.icon />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {navSecondary.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    onClick={() => handleNavigation(item.route)}
                    isActive={currentRoute === item.route}
                    className="cursor-pointer"
                  >
                    <item.icon />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={displayUser} />
      </SidebarFooter>
    </Sidebar>
  )
}