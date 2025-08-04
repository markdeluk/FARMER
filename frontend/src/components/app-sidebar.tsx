import { Calendar, HelpCircle, Home, Inbox, Search, Settings } from "lucide-react"

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
import { NavSecondary } from "./mine/nav-secondary"
import { useAuth } from "@/hooks/use-auth"

// Menu items.
const items = [
  {
    title: "Home",
    url: "#",
    icon: Home,
  },
  {
    title: "Inbox",
    url: "#",
    icon: Inbox,
  },
  {
    title: "Calendar",
    url: "#",
    icon: Calendar,
  },
  {
    title: "Search",
    url: "#",
    icon: Search,
  },
]

const navSecondary = [
  {
    title: "Settings",
    url: "#",
    icon: Settings,
  },
  {
    title: "Get Help",
    url: "#",
    icon: HelpCircle,
  },
  {
    title: "Search",
    url: "#",
    icon: Search,
  },
]

export function AppSidebar() {
  const { user, isAuthenticated } = useAuth()

  // Se l'utente non è autenticato, mostra dati di default
  const displayUser = isAuthenticated && user ? {
    name: `${user.first_name} ${user.last_name}`,
    email: user.email,
    avatar: user.profile_picture ? `data:image/jpeg;base64,${user.profile_picture}` : `https://api.dicebear.com/7.x/initials/svg?seed=${user.first_name}%20${user.last_name}`,
  } : {
    name: "Guest User",
    email: "guest@example.com", 
    avatar: "https://api.dicebear.com/7.x/initials/svg?seed=Guest%20User",
  }

  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Application</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <NavSecondary items={navSecondary} className="mt-auto" />
      </SidebarContent>
        <SidebarFooter>
          <NavUser user={displayUser} />
        </SidebarFooter>
    </Sidebar>
  )
}