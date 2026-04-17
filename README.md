# PharmaTrack - Material Depository & Request Management System

🏥 A web-based inventory and request management system for pharmaceutical companies.

## Developer
**Sree Vasthav Upputoori**

## Features

- ✅ **Material Inventory** — Track solvents, reagents, raw materials, buffers, media, lab supplies
- ✅ **Real-time Balance Tracking** — Always know your current stock levels
- ✅ **Low Stock Alerts** — Automatic warnings when inventory is running low
- ✅ **Request System** — Employees submit material requests online
- ✅ **Approval Workflow** — Managers approve/reject requests
- ✅ **Auto-Deduction** — Approved requests automatically deduct from main stock
- ✅ **Full Audit Trail** — Complete history of all transactions
- ✅ **User Management** — Role-based access (Admin, Manager, User)

## Quick Start

```bash
# Install dependencies
npm install

# Start server
npm start

# Open in browser
open http://localhost:3000
```

## Tech Stack

- **Backend:** Node.js + Express.js
- **Database:** SQLite (sql.js)
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Authentication:** JWT + bcrypt

## Materials Included (Pre-seeded)

| Category | Examples |
|---|---|
| Solvents | Methanol, Ethanol, Acetonitrile, DMSO, Chloroform, Acetone |
| Reagents | NaOH, HCl, H2SO4, KMnO4, NaCl, EDTA |
| Raw Materials | Lactose, MCC, Starch, Talc, Mg Stearate |
| Buffers | PBS, Citrate, Acetate, Tris |
| Media | LB Broth, Nutrient Agar, RPMI |
| Lab Supplies | Filter Paper, Pipette Tips, Syringes, Vials |

## Screenshots

### Dashboard
- Total materials count
- Low stock alerts
- Out of stock count
- Pending requests
- Recent transactions

### Materials Page
- Searchable/filterable inventory
- Stock status indicators (OK/Low/Out)
- Add/Edit/Adjust stock
- CAS numbers and formulas

### Requests Page
- Submit new requests
- Filter by status (Pending/Approved/Rejected)
- One-click approve/reject for managers
- Auto-deduction from stock

## API Endpoints

### Auth
- `POST /api/auth/login` — Login
- `POST /api/auth/register` — Register user (admin only)
- `GET /api/auth/me` — Get current user

### Materials
- `GET /api/materials` — List all materials
- `POST /api/materials` — Add material (admin)
- `PUT /api/materials/:id` — Update material (admin)
- `DELETE /api/materials/:id` — Delete material (admin)
- `PUT /api/materials/:id/adjust` — Adjust stock (admin)
- `GET /api/materials/alerts/low-stock` — Get low stock items

### Requests
- `GET /api/requests` — List requests
- `POST /api/requests` — Submit request
- `PUT /api/requests/:id/approve` — Approve (manager)
- `PUT /api/requests/:id/reject` — Reject (manager)

## User Roles

| Role | Permissions |
|---|---|
| **Admin** | Full access: manage materials, approve/reject requests, manage users |
| **Manager** | View materials, approve/reject requests |
| **User** | View materials, submit requests |

## Project Structure

```
pharmatrack/
├── server/
│   ├── index.js          # Express server
│   ├── database.js       # SQLite setup + seeding
│   ├── routes/
│   │   ├── auth.js       # Authentication
│   │   ├── materials.js   # Material CRUD
│   │   └── requests.js   # Request workflow
│   └── middleware/
│       └── auth.js       # JWT middleware
├── public/
│   ├── index.html        # Main SPA
│   ├── css/style.css     # Styles
│   └── js/app.js         # Frontend JS
├── package.json
└── README.md
```

## License

MIT
