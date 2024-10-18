def morton_curve(p, s, t, c, g):
        args = (p, s, t, c, g)
        max_bits = max(arg.bit_length() for arg in args)
        result = 0
        
        for i in range(max_bits):
            result |= ((p >> i) & 1) << (i * 5 + 0)
            result |= ((s >> i) & 1) << (i * 5 + 1)
            result |= ((t >> i) & 1) << (i * 5 + 2)
            result |= ((c >> i) & 1) << (i * 5 + 3)
            result |= ((g >> i) & 1) << (i * 5 + 4)
        
        return result
    
def assign_rooms(plane, ship, train, car, guest):
    with open("test_room", "w") as f:
        # Store guest assignments using consistent coordinates
        for g in range(guest):
            # Calculate some reasonable coordinates for guests
            # Here, I'm using g % plane, g % ship, etc., to derive room-like coordinates for guests
            p = g % plane
            s = (g // plane) % ship
            t = (g // (plane * ship)) % train
            c = (g // (plane * ship * train)) % car
            
            # Insert guest using calculated Morton code
            result = morton_curve(p, s, t, c, 0)
            f.write(f"{result}, old_no_{p+1}_{s+1}_{t+1}_{c+1}_{g}\n")
            print(result, f"old_no_{p+1}_{s+1}_{t+1}_{c+1}_{g}")

        total_rooms = plane * ship * train * car
        for i in range(total_rooms):
            p = (i // (ship * train * car)) % plane
            s = (i // (train * car)) % ship
            t = (i // (car)) % train
            c = (i) % car
            
            result = morton_curve(p, s, t, c, 0)
            # Insert room using calculated Morton code
            f.write(f"{result}, no_{p+1}_{s+1}_{t+1}_{c+1}_{0}\n")
            print(result, f"no_{p+1}_{s+1}_{t+1}_{c+1}_{0}")
        

assign_rooms(1,2,3,4,5)