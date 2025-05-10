import { Button } from "@/components/ui/button";
import { ThemeToggle } from "./ThemeToggle";
import { Bell, User } from "lucide-react";

export function Navbar() {
  return (
    <header className="bg-whatsapp-darkGreen text-white p-4 shadow-md">
      <div className="w-full flex items-center justify-between">
        <div className="flex items-center gap-2">
          <h1 className="text-xl font-bold">WhatsApp Management</h1>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5" />
          </Button>

          <ThemeToggle />

          <Button variant="ghost" size="icon">
            <User className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
}